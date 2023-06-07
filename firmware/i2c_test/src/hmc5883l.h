#ifndef HCM5883L_H
#define HCM5883L_H

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/logging/log.h>
#include <zephyr/math/ilog2.h>
#include <math.h>
#include "config.h"

// #define HMC_i2c_addr 	0x7E
#define HMC_i2c_addr 	(0b0111100)
#define HMC_i2c_addr 	(0x3C >> 1)
#define HMC_i2c_addr 	(0x1E)


#define HMC_CONFIG_REG_A    0
#define HMC_CONFIG_REG_B    1
#define HMC_MODE_REG        2
#define HMC_X_HIGH          3
#define HMC_X_LOW           4
#define HMC_Y_HIGH          5
#define HMC_Y_LOW           6
#define HMC_Z_HIGH          7
#define HMC_Z_LOW           8
#define HMC_STATUS_REG      9
#define HMC_ID_REG_A        10
#define HMC_ID_REG_B        11
#define HMC_ID_REG_C        12

#define HMC_DATA_START HMC_X_HIGH

typedef enum {
    continuous = 0b00,
    single = 0b01,
    idle = 0b11
} HMC_mode_t;

uint8_t HMC_init(const struct device *i2c_device);
uint8_t HMC_read_mag(int16_t output[]);
uint8_t HMC_set_mode(HMC_mode_t mode, bool high_speed);

#endif