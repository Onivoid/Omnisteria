migrate:
	docker exec -it ${containerID} aerich migrate
upgrade:
	docker exec -it ${containerID} aerich upgrade
runall:
	docker exec -it ${containerID} aerich migrate && docker exec -it ${containerID} aerich upgrade