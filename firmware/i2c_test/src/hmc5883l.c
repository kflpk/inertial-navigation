#include "hmc5883l.h"
#include <zephyr/logging/log.h>

// FIX: I2C communication works but data doesn't update
// FIX: I2C breaks when sensor is shaken too much
/*
    TODO: Try sending 3D and 3C as a first packet before transmitting data
    Things to try:
    - [ ] Split the config transmissions to one byte messages
    - [ ] try the high-speed I2C mode for HMC
    - [ ] Configure MPU auxillary I2C bus to master
*/

static struct device *i2c_dev;
static uint8_t i2c_buffer[64];

LOG_MODULE_REGISTER(HMC5883L);

uint8_t HMC_init(const struct device *i2c_device)
{
    i2c_dev = i2c_device;
    uint8_t ret;

    LOG_DBG("initializing HMC");

    i2c_buffer[0] = HMC_CONFIG_REG_A;
    // i2c_buffer[1] = (0b00 << 0) | (0b100 << 2) | (0b00 << 5);
    i2c_buffer[1] = 0x70;
    ret = i2c_write(i2c_dev, i2c_buffer, 2, HMC_i2c_addr);
    if (ret)
    {
        LOG_ERR("Couldn't write to HMC_CONFIG_REG_A, ret: %d", ret);
        return ret;
    }

    i2c_buffer[0] = HMC_CONFIG_REG_B;
    // i2c_buffer[1] = (0b000 << 5);
    i2c_buffer[1] = 0xA0;
    i2c_write(i2c_dev, i2c_buffer, 2, HMC_i2c_addr);
    if (ret) {
        LOG_ERR("Couldn't write to HMC_CONFIG_REG_B, ret: %d", ret);
        return ret;
    }

    ret = HMC_set_mode(continuous, false);
    if (ret) {
        LOG_ERR("Couldn't set mode of HMC, ret: %d", ret);
        return ret;
    }

    LOG_DBG("HMC initialized");

    return 0;
}

uint8_t HMC_read_mag(int16_t output[])
{
    int ret;

    i2c_buffer[0] = HMC_DATA_START;
    ret = i2c_write(i2c_dev, i2c_buffer, 1, HMC_i2c_addr);
    if(ret) {
        return ret;
    }

    ret = i2c_read(i2c_dev, i2c_buffer, 6, HMC_i2c_addr);
    if (ret)
    {
        return ret;
    }

    for (uint8_t i = 0; i < 3; i++)
    {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }
}

uint8_t HMC_set_mode(HMC_mode_t mode, bool high_speed)
{
    uint8_t ret;
    uint8_t mode_val = high_speed ? 0b11111100 : 0b00000000;
    mode_val |= (uint8_t)mode;
    LOG_DBG("mode_val=%d", (uint8_t)mode_val);

    i2c_buffer[0] = HMC_MODE_REG;
    i2c_buffer[1] = mode_val;
    ret = i2c_write(i2c_dev, i2c_buffer, mode_val, HMC_i2c_addr);

    return ret;
}
