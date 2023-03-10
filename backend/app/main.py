from logging.config import dictConfig

import uvicorn
import logging
from fastapi import FastAPI, HTTPException

from controller import Controller
from config import Settings, LogConfig

MODULATIONS = ['FM', 'AM', 'NFM', 'WFM_ST', 'WFM_ST_OIRT', 'WFM']

settings = Settings()

dictConfig(LogConfig().dict())
logger = logging.getLogger('gqrx')

app = FastAPI(
    debug=settings.environment == 'dev',
    title=settings.title,
    description=settings.description,
    version=settings.version,
)

controller = Controller()


@app.get("/", response_model=None)
async def index():
    global controller
    return {"controller": controller}


@app.patch("/", response_model=None)
async def index(options: Controller):
    global controller
    controller_data = options.dict(exclude_unset=True)

    (freq, mod) = (
        controller_data.get('freq', None),
        controller_data.get('mod', None)
    )

    if controller.active and (freq or mod):
        if freq:
            res = await controller.send('F', freq)
            if '0' in res:
                logger.info("Freq: " + freq)
            else:
                logger.error("Freq error")
                raise HTTPException(status_code=503, detail="Error changing frequency")

        if mod:
            res = await controller.send('M', mod)
            if '0' in res:
                logger.info("Mod: " + mod)
            else:
                logger.error("Mod error")
                raise HTTPException(status_code=503, detail="Error changing modulation")

        controller = controller.copy(update=controller_data)
    return {"controller": controller}


@app.post('/connect', response_model=None)
async def connect(options: Controller):
    global controller
    controller_data = options.dict(exclude_unset=True)
    active = controller_data.get('active', None)

    if active:
        res = await controller.connect()
        if not res:
            logger.error('Cannot connect')
            raise HTTPException(status_code=503, detail="GQRX source unavailable")
        return {"controller": controller}
    else:
        raise HTTPException(status_code=503, detail="GQRX source unavailable")

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
