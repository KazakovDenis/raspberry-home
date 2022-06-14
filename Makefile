precommit:
	poetry run isort -c .
	poetry run pflake8

agent_deploy:
	scp control/cmd_agent/agent.py pi:
	ssh -t pi "sudo mv agent.py /opt/cmd_agent && sudo systemctl restart cmd_agent"

BOT_ARCHIVE="bot.tar.gz"
BOT_IMAGE="control_bot:latest"
BOT_TMP="bot.img"
BOT_LOCAL_COMPOSE="control/docker-compose.yml"
BOT_REMOTE_COMPOSE="/opt/control_bot/docker-compose.yml"
WIREHOLE_LOCAL_COMPOSE="wirehole/wirehole/docker-compose.yml"
WIREHOLE_REMOTE_COMPOSE="/opt/wirehole/docker-compose.yml"

bot_build:
	docker compose -f ${BOT_LOCAL_COMPOSE} build bot
	docker save ${BOT_IMAGE} -o ${BOT_TMP}
	tar -czvf ${BOT_ARCHIVE} ${BOT_TMP}
	rm ${BOT_TMP}

bot_deploy:
	scp ${BOT_ARCHIVE} vps:
	ssh -t vps "\
		tar -xvf ${BOT_ARCHIVE} && \
		docker load -i ${BOT_TMP} && \
		rm ${BOT_TMP} ${BOT_ARCHIVE} \
	"
	ssh -t vps "docker-compose -f ${WIREHOLE_REMOTE_COMPOSE} -f ${BOT_REMOTE_COMPOSE} up -d --force-recreate bot"
