migrate:
	docker exec -it ${CID} aerich migrate
upgrade:
	docker exec -it ${CID} aerich upgrade
runall:
	docker exec -it ${CID} aerich migrate && docker exec -it ${CID} aerich upgrade