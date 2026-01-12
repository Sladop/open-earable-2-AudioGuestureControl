
#include "../buttons/button_manager.h"
#include <zephyr/zbus.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(my_button_handler, LOG_LEVEL_DBG);

void my_button_cb(const struct zbus_channel *chan, const void *msg)
{
    const struct button_msg *button = (const struct button_msg *)msg;

    if (button->pin == BUTTON_EARABLE) {
        LOG_INF("Earable Button gedrückt!");
    }
}

void subscribe_to_button() {
    zbus_chan_subscribe(&button_chan, my_button_cb, ZBUS_OBSERVERS_ANY);
}
