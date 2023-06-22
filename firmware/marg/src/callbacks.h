#ifndef CALLBACKS_H
#define CALLBACKS_H

#include "remote.h"

void on_connected(struct bt_conn* conn, uint32_t err);
void on_disconnected(struct bt_conn* conn, uint32_t reason);

#endif