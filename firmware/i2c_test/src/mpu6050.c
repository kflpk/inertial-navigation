#include "mpu6050.h"

static struct device *i2c_dev;
static uint8_t i2c_buffer[6];

uint8_t MPU_init(const struct device *i2c_device) {
    // TODO: make this prettier
    i2c_dev = i2c_device;

    i2c_buffer[0] = SMPLRT_DIV_REG;
    i2c_buffer[1] = 7;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = PWR_MGMT_1_REG;
    i2c_buffer[1] = 1;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = CONFIG_REG;
    i2c_buffer[1] = 0;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = GYRO_CONFIG_REG;
    i2c_buffer[1] = 24;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = ACC_CONFIG_REG;
    i2c_buffer[1] = AFS_SEL << 3;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = GYRO_CONFIG_REG;
    i2c_buffer[1] = FS_SEL << 3;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    i2c_buffer[0] = INT_ENABLE_REG;
    i2c_buffer[1] = 1;
    i2c_write(i2c_dev, i2c_buffer, 2, MPU_i2c_addr);

    return 0;
}

uint8_t MPU_read_acc(int16_t output[3]) {
    i2c_buffer[0] = ACC_REG_START;

    uint8_t ret = i2c_write(i2c_dev, i2c_buffer, 1, MPU_i2c_addr);

    if(ret) {
        return ret;
    }

    ret = i2c_read(i2c_dev, i2c_buffer, 6, MPU_i2c_addr);
    if(ret) {
        return ret;
    }

    for(uint8_t i = 0; i < 3; i++) {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }

    return 0;
}

// FIX: this absolutely violated the DRY rule, but i can fix it later
uint8_t MPU_read_gyro(int16_t output[]) {
    i2c_buffer[0] = GYRO_REG_START;

    uint8_t ret = i2c_write(i2c_dev, i2c_buffer, 1, MPU_i2c_addr);

    if(ret) {
        return ret;
    }

    ret = i2c_read(i2c_dev, i2c_buffer, 6, MPU_i2c_addr);
    if(ret) {
        return ret;
    }

    for(uint8_t i = 0; i < 3; i++) {
        output[i] = (i2c_buffer[2 * i] << 8) | i2c_buffer[2 * i + 1];
    }

    return 0;
}