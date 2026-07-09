# all of the publish and status messaging commands

# http://www.steves-internet-guide.com/client-connections-python-mqtt/

import paho.mqtt.client as paho
import json
import time
import logging
import uuid

logger = logging.getLogger("messaging")

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


class Messaging:

    def __init__(self) -> None:
        self.connected = False
        self.client = None
        self.topic_handlers = {}
        self.server = ""
        self.subscribe_qos = 1
        self.loop_started = False

    # ----------------------------------------------------------------------------
    def on_disconnect(self, client, userdata, rc, properties):
        """
        MQTT on_disconnect callback for MQTT v5.
        """
        self.connected = False
        if rc == 0:
            logger.info("MQTT disconnected normally")
        else:
            logger.warning("Unexpected MQTT disconnection (%s). Will auto-reconnect", rc)


    def on_disconnect_retry(self, client, userdata, rc, properties):
        logger.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logger.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                self.client.reconnect()
                logger.info("Reconnected successfully!")
                return
            except Exception as err:
                logger.error("%s. Reconnect failed. Retrying...", err)

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
            # logger.info("Connected to MQTT Broker!")
            # Subscribe to known multiple topics
            for topic, handler in self.topic_handlers.items():
                self.client.subscribe(topic, qos=self.subscribe_qos)
            # Catch anything else
            self.client.subscribe("#", qos=self.subscribe_qos)
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

            try:
                self.topic_handlers[topic](topic=topic, data=json.loads(message.payload.decode()))
            except Exception as err:
                logger.info( f"likely message is not JSON topic:{topic}, message:{message.payload.decode()}")
                logger.info(f"{type(err).__name__} was raised eventually in topics_on_message: {err}")
        # else:
        #     self.handle_all(client, userdata, message)


    # ----------------------------------------------------------------------------
    # pass topic handlers if we are in a subscription kinda mood,
    # will then loop forever waiting for topics to be pubished


    def connect(self, handlers=None, server="localhost", port=1883, client_id=None, clean_session=True, subscribe_qos=1):
        """
        Connect to MQTT server with exponential backoff retry.
        Useful for Raspberry Pi startups where MQTT service may not be ready immediately.
        """
        self.server = server
        self.subscribe_qos = subscribe_qos
        
        self.loop_started = False
        
        # logger.debug(f"Connecting to MQTT server: {server}:{port}")

        self.client = paho.Client(
            paho.CallbackAPIVersion.VERSION2,
            client_id=client_id or f"status-{uuid.uuid4().hex[:8]}",
            clean_session=clean_session,
        )
        self.client.reconnect_delay_set(FIRST_RECONNECT_DELAY, MAX_RECONNECT_DELAY)
        # logger.debug("MQTT client created")
        # if we need a username and password
        # client.username_pw_set(server, pwd)

        # Retry logic with exponential backoff
        reconnect_count = 0
        reconnect_delay = FIRST_RECONNECT_DELAY
        
        while reconnect_count < MAX_RECONNECT_COUNT:
            try:
                # keep alive is 300s
                if self.client.connect(server, port, 300) == 0:
                    self.connected = True
                    logger.info(f"Re-connected to MQTT server: {server}:{port}")
                    break
                else:
                    raise Exception(f"Connection failed with return code {self.client._sock}")
            except Exception as err:
                reconnect_count += 1
                if reconnect_count >= MAX_RECONNECT_COUNT:
                    logger.error(f"Couldn't connect to the MQTT server after {reconnect_count} attempts: {err}")
                    self.connected = False
                    break
                logger.warning(f"Connection attempt {reconnect_count} failed: {err}. Retrying in {reconnect_delay}s...")
                time.sleep(reconnect_delay)
                reconnect_delay *= RECONNECT_RATE
                reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)

        # Attach callbacks before starting the network loop.
        self.client.on_disconnect = self.on_disconnect
        if handlers:
            self.topic_handlers = handlers
            self.client.on_connect = self.topics_on_connect
            self.client.on_message = self.topics_on_message
        else:
            self.client.on_connect = self.on_connect

        # now to the subscription loop
        if handlers and self.connected:
            self.client.loop_forever()
        elif self.connected and not self.loop_started:
            # Publisher-only clients still need a network loop to process outgoing packets.
            self.client.loop_start()
            self.loop_started = True


    # ----------------------------------------------------------------------------
    def publish(self, subtopic, data=None, retain=False):
        """
        Publish a message with optional MQTT QoS and retained delivery settings.
        """
        if data is None:
            data = {}

        # attempt a reconnect if needed
        if not self.connected:
            self.connect()

        if self.connected:
            # time in seconds since epoch
            data["_epoch"] = int(time.time())
            stats = self.client.publish(f"{subtopic}", json.dumps(data), qos=1, retain=retain)
            # logger.debug(f"Published to {subtopic}: {data}, stats {stats}")
        else:
            logger.error(f"Failed to publish to {subtopic}: Not connected to MQTT server")


    def on_publish(self, client, userdata, mid):
        logger.debug(f"Message {mid} published successfully.")

    # ----------------------------------------------------------------------------
    def client_disconnect(self):
        """
        """
        if self.connected:
            self.client.disconnect()


