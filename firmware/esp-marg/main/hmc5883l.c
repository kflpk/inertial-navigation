#include "hmc5883l.h"
// #include <zephyr/logging/log.h>

static uint8_t i2c_buffer[64];

// LOG_MODULE_REGISTER(HMC5883L);
static char log_module_name[] = "HMC5883L";

uint8_t HMC_init() {
    uint8_t ret = 0;
    uint8_t config_reg_a[2] = {HMC_CONFIG_REG_A, 0x70};
    uint8_t config_reg_b[2] = {HMC_CONFIG_REG_B, (HMC_GAIN << 5)};

    ESP_LOGI(log_module_name, "initializing HMC");

    // i2c_buffer[1] = (0b00 << 0) | (0b100 << 2) | (0b00 << 5);
    // ret = i2c_write(i2c_dev, config_reg_a, 2, HMC_i2c_addr);
    i2c_master_write_to_device(I2C_NUM, HMC_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    if (ret)
    {
        ESP_LOGE(log_module_name, "Couldn't write to HMC_CONFIG_REG_A, ret: %d", ret);
        return ret;
    }

    // i2c_buffer[1] = (0b000 << 5);
    // i2c_write(i2c_dev, config_reg_b, 2, HMC_i2c_addr);
    i2c_master_write_to_device(I2C_NUM, HMC_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    if (ret) {
        ESP_LOGE(log_module_name, "Couldn't write to HMC_CONFIG_REG_B, ret: %d", ret);
        return ret;
    }

    ret = HMC_set_mode(continuous, false);
    if (ret) {
        ESP_LOGE(log_module_name, "Couldn't set mode of HMC, ret: %d", ret);
        return ret;
    }

    ESP_LOGI(log_module_name, "HMC initialized");

    return 0;
}

uint8_t HMC_read_mag(int16_t output[]) {
    int ret = 0;

    uint8_t data_start_reg[1] = {HMC_DATA_START};
    uint8_t data[6];

    // ret = i2c_write(i2c_dev, data_start_reg, 1, HMC_i2c_addr);
    // if(ret) {
    //     return ret;
    // }

    // ret = i2c_read(i2c_dev, data, 6, HMC_i2c_addr);
    // if (ret)
    // {
    //     return ret;
    // }
    i2c_master_write_read_device(I2C_NUM, HMC_i2c_addr, data_start_reg, 1, data, 6, I2C_TIMEOUT);

    for (uint8_t i = 0; i < 3; i++) {
        output[i] = (data[2 * i] << 8) | (data[2 * i + 1]);
    }

    return ret;
}

uint8_t HMC_set_mode(HMC_mode_t mode, bool high_speed) {
    esp_err_t err = ESP_OK;
    uint8_t mode_val = high_speed ? 0b11111100 : 0b00000000;
    mode_val |= (uint8_t)mode;
    uint8_t mode_reg[2] = {HMC_MODE_REG, mode_val};

    // ret = i2c_write(i2c_dev, mode_reg, 2, HMC_i2c_addr);
    err = i2c_master_write_to_device(I2C_NUM, HMC_i2c_addr, mode_reg, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    return err;
}

uint8_t HMC_get_status() {
    uint8_t status, err = ESP_OK;
    uint8_t status_reg[1] = {HMC_STATUS_REG};

    // i2c_write(i2c_dev, status_reg, 1, HMC_i2c_addr);

    // i2c_read(i2c_dev, i2c_buffer, 1, HMC_i2c_addr);
    err = i2c_master_write_read_device(I2C_NUM, HMC_i2c_addr, status_reg, 1, i2c_buffer, 1, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    status = i2c_buffer[0];

    return status;
}

uint8_t HMC_set_gain(uint8_t gain) {
    uint8_t config_reg_b[2] = { HMC_CONFIG_REG_B, (gain << 5) };
    // return i2c_write(i2c_dev, config_reg_b, 2, HMC_i2c_addr);
    return i2c_master_write_to_device(I2C_NUM, HMC_i2c_addr, config_reg_b, 2, I2C_TIMEOUT);
}

uint8_t HMC_get_gain(void) {
    uint8_t* gain;
    uint8_t config_reg_b[1] = { HMC_CONFIG_REG_B };
    
    // i2c_write(i2c_dev, config_reg_b, 1, HMC_i2c_addr);
    // i2c_read(i2c_dev,  gain,         1, HMC_i2c_addr);
    i2c_master_write_read_device(I2C_NUM, HMC_i2c_addr, config_reg_b, 1, &gain, 1, I2C_TIMEOUT);

    return *gain;
}
