#include "hmc5883l.h"
#include <zephyr/logging/log.h>

static struct device *i2c_dev;
static uint8_t i2c_buffer[64];

LOG_MODULE_REGISTER(HMC5883L);

uint8_t HMC_init(const struct device *i2c_device)
{
    i2c_dev = i2c_device;

    uint8_t ret;
    uint8_t config_reg_a[2] = {HMC_CONFIG_REG_A, 0x70};
    uint8_t config_reg_b[2] = {HMC_CONFIG_REG_B, (HMC_GAIN << 5)};

    LOG_DBG("initializing HMC");

    // i2c_buffer[1] = (0b00 << 0) | (0b100 << 2) | (0b00 << 5);
    ret = i2c_write(i2c_dev, config_reg_a, 2, HMC_i2c_addr);
    if (ret)
    {
        LOG_ERR("Couldn't write to HMC_CONFIG_REG_A, ret: %d", ret);
        return ret;
    }

    // i2c_buffer[1] = (0b000 << 5);
    i2c_write(i2c_dev, config_reg_b, 2, HMC_i2c_addr);
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

    uint8_t data_start_reg[1] = {HMC_DATA_START};
    uint8_t data[6];

    ret = i2c_write(i2c_dev, data_start_reg, 1, HMC_i2c_addr);
    if(ret) {
        return ret;
    }

    ret = i2c_read(i2c_dev, data, 6, HMC_i2c_addr);
    if (ret)
    {
        return ret;
    }

    for (uint8_t i = 0; i < 3; i++) {
        output[i] = (data[2 * i] << 8) | (data[2 * i + 1]);
    }
}

uint8_t HMC_set_mode(HMC_mode_t mode, bool high_speed) {
    uint8_t ret;
    uint8_t mode_val = high_speed ? 0b11111100 : 0b00000000;
    mode_val |= (uint8_t)mode;
    uint8_t mode_reg[2] = {HMC_MODE_REG, mode_val};

    ret = i2c_write(i2c_dev, mode_reg, 2, HMC_i2c_addr);

    return ret;
}

uint8_t HMC_get_status() {
    uint8_t status, ret;
    uint8_t status_reg[1] = {HMC_STATUS_REG};

    i2c_write(i2c_dev, status_reg, 1, HMC_i2c_addr);

    i2c_read(i2c_dev, i2c_buffer, 1, HMC_i2c_addr);

    status = i2c_buffer[0];

    return status;
}

uint8_t HMC_set_gain(uint8_t gain) {
    uint8_t config_reg_b[2] = { HMC_CONFIG_REG_B, (gain << 5) };
    return i2c_write(i2c_dev, config_reg_b, 2, HMC_i2c_addr);
}

uint8_t HMC_get_gain(void) {
    uint8_t* gain;
    uint8_t config_reg_b[1] = { HMC_CONFIG_REG_B };
    
    i2c_write(i2c_dev, config_reg_b, 1, HMC_i2c_addr);
    i2c_read(i2c_dev,  gain,         1, HMC_i2c_addr);

    return *gain;
}
