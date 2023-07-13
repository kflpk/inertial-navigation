#include "mpu6050.h"

static char log_module_name[] = "MPU6050";

static uint8_t i2c_buffer[6];

uint8_t MPU_init(void) {
    // TODO: make this prettier
    int err = ESP_OK;

    ESP_LOGI(log_module_name, "Initializing MPU6050");
    i2c_buffer[0] = SMPLRT_DIV_REG;
    i2c_buffer[1] = 7;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = PWR_MGMT_1_REG;
    i2c_buffer[1] = 1;
    err =i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = CONFIG_REG;
    i2c_buffer[1] = 0;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = GYRO_CONFIG_REG;
    i2c_buffer[1] = 24;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = ACC_CONFIG_REG;
    i2c_buffer[1] = AFS_SEL << 3;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = GYRO_CONFIG_REG;
    i2c_buffer[1] = FS_SEL << 3;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = INT_ENABLE_REG;
    i2c_buffer[1] = 1;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    // Enable I2C pass-through mode
    i2c_buffer[0] = INT_PIN_CFG_REG;
    i2c_buffer[1] = (1 << I2C_BYPASS_EN);
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    i2c_buffer[0] = USER_CTRL_REG;
    i2c_buffer[1] = 0;
    err = i2c_master_write_to_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 2, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    ESP_LOGI(log_module_name, "MPU6050 initialized");

    return 0;
}

uint8_t MPU_read_acc(int16_t output[]) {
    i2c_buffer[0] = ACC_REG_START;

    // uint8_t ret = i2c_write(i2c_dev, i2c_buffer, 1, MPU_i2c_addr);

    // if(ret) {
    //     return ret;
    // }

    // ret = i2c_read(i2c_dev, i2c_buffer, 6, MPU_i2c_addr);
    // if(ret) {
    //     return ret;
    // }

    esp_err_t err = i2c_master_write_read_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 1, i2c_buffer, 6, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    for(uint8_t i = 0; i < 3; i++) {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }

    return 0;
}

// FIX: this absolutely violated the DRY rule, but i can fix it later
uint8_t MPU_read_gyro(int16_t output[]) {
    i2c_buffer[0] = GYRO_REG_START;

    // uint8_t ret = i2c_write(i2c_dev, i2c_buffer, 1, MPU_i2c_addr);

    // if(ret) {
    //     return ret;
    // }

    // ret = i2c_read(i2c_dev, i2c_buffer, 6, MPU_i2c_addr);
    // if(ret) {
    //     return ret;
    // }

    uint8_t err = i2c_master_write_read_device(I2C_NUM, MPU_i2c_addr, i2c_buffer, 1, i2c_buffer, 6, I2C_TIMEOUT);
    ESP_ERROR_CHECK(err);

    for(uint8_t i = 0; i < 3; i++) {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }

    return 0;
}