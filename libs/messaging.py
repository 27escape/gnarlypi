# all of the publish and subscript messaging commands

# http://www.steves-internet-guide.com/client-connections-python-mqtt/

import paho.mqtt.client as paho
import json
import time
import logging

logger = logging.getLogger(__name__)

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


class Messaging:

    def __init__(self) -> None:
        self.connected = False
        self.client = None
        self.topic_handlers = {}
        self.server =  ""


    # ----------------------------------------------------------------------------
    def on_disconnect(self, client, userdata, rc):
        """
        """
        print("on disconnect")
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")


    def on_disconnect_retry(self, client, userdata, rc):
        logger.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logger.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                self.client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logger.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


    # ----------------------------------------------------------------------------


    def handle_all(self, client, userdata, message):
        """
        """
        # Access sensor data based on the structure of your data
        # (e.g., data["sensor_type"], data["value"])
        logger.debug(f"ALL: catchall: {json.loads(message.payload.decode())} (topic: {message.topic})")


    # ----------------------------------------------------------------------------


    def on_connect(self, client, userdata, flags, reason_code, properties):
        """
        """
        if reason_code == 0:
            logger.info(f"Connected to MQTT server: {self.server}")
        else:
            logger.debug("Failed to connect, return code: {}".format(reason_code))


    # ----------------------------------------------------------------------------
    def topics_on_connect(self, client, userdata, flags, reason_code, properties):
        """
        """
        if reason_code == 0:
            logger.info("Connected to MQTT Broker!")
            # Subscribe toknown  multiple topics
            for topic, handler in self.topic_handlers.items():
                self.client.subscribe(topic, qos=1)
            #  catch anything else
            self.client.subscribe("#", qos=1)
        else:
            logger.info("Failed to connect, return code: {}".format(reason_code))


    # ----------------------------------------------------------------------------
    def topics_on_message(self, client, userdata, message):
        """
        """
        # Identify topic and call appropriate handler function
        # we will ignore the user data and pull out the payload
        # for this usecase not much else is needed
        topic = message.topic
        if topic in self.topic_handlers:
            self.topic_handlers[topic](topic=message.topic, data=json.loads(message.payload.decode()))
        else:
            self.handle_all(client, userdata, message)


    # ----------------------------------------------------------------------------
    # pass topic handlers if we are in a subscription kinda mood,
    # will then loop forever waiting for topics to be pubished


    def connect(self, handlers=None, server="localhost", port=1883):
        """
        """
        self.server = server

        self.client = paho.Client(paho.CallbackAPIVersion.VERSION2)
        # if we need a username and password
        # client.username_pw_set(server, pwd)

        # keep alive is 300s
        if self.client.connect(server, port, 300) != 0:
            logger.error(f"Couldn't connect to the MQTT server: {server}")
            self.connected = False
        else:
            self.connected = True

        # put these after the connect, so that they subscribe after re-connecting
        self.client.on_disconnect = self.on_disconnect
        if handlers:
            self.topic_handlers = handlers
            self.client.on_connect = self.topics_on_connect
            self.client.on_message = self.topics_on_message
        else:
            self.client.on_connect = self.on_connect

        # now to the subscription loop
        if handlers:
            self.client.loop_forever()


    # ----------------------------------------------------------------------------
    def publish(self, subtopic, data={}):
        """
        """

        # attempt a reconnect if needed
        if not self.connected:
            self.connect()

        if self.connected:
            data["_epoch"] = time.time()
            self.client.publish(f"{subtopic}",  json.dumps(data))


    # ----------------------------------------------------------------------------
    def client_disconnect(self):
        """
        """
        if self.connected:
            self.client.disconnect()


