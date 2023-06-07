#include "hmc5883l.h"
#include <zephyr/logging/log.h>

static struct device *i2c_dev;
static uint8_t i2c_buffer[6];

LOG_MODULE_REGISTER(HMC5883L);

// FIX: I CAN'T CONNECT TO THIS GOD DAMN SENSOR

uint8_t HMC_init(const struct device *i2c_device) {
    i2c_dev = i2c_device;
    uint8_t ret;

    LOG_DBG("initializing HMC");

    i2c_buffer[0] = HMC_CONFIG_REG_A;
    i2c_buffer[1] = 0x71;
    ret = i2c_write(i2c_dev, i2c_buffer, 2, HMC_i2c_addr);
    if(ret) {
        LOG_ERR("Error while initializing HMC");
        return ret;
    }

    i2c_buffer[0] = HMC_CONFIG_REG_B;
    // i2c_buffer[1] = 0b00100000;
    i2c_buffer[1] = 0xA0;
    i2c_write(i2c_dev, i2c_buffer, 2, HMC_i2c_addr);
    if(ret) {
        LOG_ERR("Error while initializing HMC");
        return ret;
    }

    ret = HMC_set_mode(continuous, false);
    if(ret) {
        LOG_ERR("Error while initializing HMC");
        return ret;
    }

    LOG_DBG("HMC initialized");

    return 0;
}

// uint8_t HMC_read_mag(int16_t output[]) {
//     int ret;

//     i2c_buffer[0] = HMC_DATA_START;

//     ret = i2c_write(i2c_dev, i2c_buffer, 1, HMC_i2c_addr);

//     if(ret) {
//         return ret;
//     }

//     ret = i2c_read(i2c_dev, i2c_buffer, 6, HMC_i2c_addr);
//     if(ret) {
//         return ret;
//     }

//     for(uint8_t i = 0; i < 3; i++) {
//         output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
//     }
// }

uint8_t HMC_set_mode(HMC_mode_t mode, bool high_speed) {
    uint8_t ret;
    uint8_t mode_val = high_speed ? 0b11111100 : 0b00000000;
    mode_val |= (uint8_t)mode;

    i2c_buffer[0] = HMC_MODE_REG;
    i2c_buffer[1] = mode_val;
    ret = i2c_write(i2c_dev, i2c_buffer, mode_val, HMC_i2c_addr);

    return ret;
}

uint8_t HMC_read_mag(int16_t output[]) {
    int ret;

    for(int i = 0; i < 6; i++) {
        LOG_DBG("i = %d", i);
        i2c_buffer[0] = HMC_DATA_START + i;
        ret = i2c_write(i2c_dev, i2c_buffer, 1, HMC_i2c_addr);

        if(ret) {
            return ret;
        }

        ret = i2c_read(i2c_dev, i2c_buffer + i, 1, HMC_i2c_addr);

        if(ret) {
            return ret;
        }
    }

    for(uint8_t i = 0; i < 3; i++) {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }

    return 0;
}