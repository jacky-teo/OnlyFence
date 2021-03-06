import json
import os

import amqp_setup

monitorBindingKey = '#'


def postMadeLog():
    amqp_setup.check_setup()

    queue_name = 'Activity_Log'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an activity log by " + __file__)
    processPostLog(json.loads(body))
    print()  # print a new line feed


def processPostLog(activity):
    print("Recording an activity log:")
    print(activity)


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    postMadeLog()
