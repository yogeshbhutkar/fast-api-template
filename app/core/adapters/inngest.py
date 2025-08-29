import logging

import inngest

inngest_client = inngest.Inngest(
	app_id="fastapi-template",
	logger=logging.getLogger("uvicorn"),
	api_base_url="http://host.docker.internal:8288",
)
