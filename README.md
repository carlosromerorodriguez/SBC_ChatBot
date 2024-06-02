# Instruccions per Configurar l'Entorn de Desenvolupament

Aquesta guia et proporcionarà els passos necessaris per configurar el teu entorn de desenvolupament.

## Creació de l'Entorn Virtual

Per crear un entorn virtual, executa el següent comandament en la terminal al directori del projecte:

```bash
python -m venv env
```

Això crearà una carpeta `env` en el teu directori actual, on s'instal·laran totes les dependències.

## Activació de l'Entorn Virtual

Per activar l'entorn virtual, utilitza el següent comandament:

### Windows
```bash
env\Scripts\activate
```

### MacOS/Linux
```bash
source env/bin/activate
```

## Instal·lació de Dependències

Un cop l'entorn virtual estigui activat, pots instal·lar les dependències requerides amb:

```bash
cd Chatbot
```
```bash
pip install -r requirements.txt
```
## Com executar el projecte
Un cop preparat l'entorn, accedeixes a aquest link a internet: [Telegram Bot](https://t.me/exploryst_bot )
Un cop estiguis en el chat del bot, en la terminal del projecte s'ha d'executar la següent comanda:
```bash
python bot.py
```
Això farà que el bot comenci a funcionar i puguis interactuar amb ell.
## Desactivació de l'Entorn Virtual

Per sortir de l'entorn virtual, pots utilitzar:

```bash
deactivate
```

Gràcies per configurar el teu entorn de desenvolupament!
