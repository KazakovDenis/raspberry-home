precommit:
	poetry run isort -c .
	poetry run pflake8

agent_deploy:
	scp control_unit/cmd_agent/agent.py pi:
	ssh -t pi "sudo mv agent.py /opt/cmd_agent && sudo systemctl restart cmd_agent"

DIST_DIR="_dist"
BOT_IMAGE="control_unit_bot:latest"
BOT_TMP="bot.img"
BOT_ARCHIVE="bot.tar.gz"
TMP_COMPOSE="bot.yml"

BOT_DEV_COMPOSE="control_unit/docker-compose.override.yml"
BOT_LOCAL_COMPOSE="control_unit/docker-compose.yml"
BOT_REMOTE_COMPOSE="/opt/control_unit/docker-compose.yml"

WIREHOLE_LOCAL_COMPOSE="wirehole/docker-compose.yml"
WIREHOLE_REMOTE_COMPOSE="/opt/wirehole/docker-compose.yml"

bot_config_dev:
	cd control_unit && docker compose config | tee _dev.yml 1>/dev/null

bot_config_prod:
	docker compose --profile prod -f ${WIREHOLE_LOCAL_COMPOSE} -f ${BOT_LOCAL_COMPOSE} config | tee _prod.yml 1>/dev/null

bot_build:
	docker compose -f ${BOT_LOCAL_COMPOSE} -f ${BOT_DEV_COMPOSE} build bot
	docker save ${BOT_IMAGE} -o ${DIST_DIR}/${BOT_TMP}
	cp ${BOT_LOCAL_COMPOSE} ${DIST_DIR}/${TMP_COMPOSE}
	tar -czvf ${DIST_DIR}/${BOT_ARCHIVE} ${DIST_DIR}/${BOT_TMP} ${DIST_DIR}/${TMP_COMPOSE}
	rm ${DIST_DIR}/${BOT_TMP} ${DIST_DIR}/${TMP_COMPOSE}

PROD_COMPOSE="docker compose -f ${WIREHOLE_REMOTE_COMPOSE} -f ${BOT_REMOTE_COMPOSE} --profile prod"

bot_deploy:
	scp ${DIST_DIR}/${BOT_ARCHIVE} vps:
	ssh -t vps "\
		tar -xvf ${BOT_ARCHIVE} && \
		${PROD_COMPOSE} rm --stop bot && \
		docker rmi ${BOT_IMAGE} && \
		docker load -i ${DIST_DIR}/${BOT_TMP} && \
		sudo mv ${DIST_DIR}/${TMP_COMPOSE} ${BOT_REMOTE_COMPOSE} && \
		rm -r ${DIST_DIR} ${BOT_ARCHIVE} && \
		${PROD_COMPOSE} up -d --force-recreate bot \
	"
