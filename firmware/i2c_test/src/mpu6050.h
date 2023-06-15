#ifndef MPU6050_H
#define MPU6050_H

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/logging/log.h>
#include <zephyr/math/ilog2.h>
#include <math.h>
#include "config.h"


#define AD0 0
#define MPU_i2c_addr 	0b1101000 | (AD0)

#define PWR_MGMT_1_REG  0x6B
#define SMPLRT_DIV_REG  0x19
#define CONFIG_REG      0x1A
#define INT_ENABLE_REG  0x38

// ======= ACCELEROMETER ======= //
// Accelerometer range
#define AFS_SEL 1
/*
     @brief sensitivity scale factor in LSB per g
*/
#define ACC_LSB_PER_G (16384.0f / pow(2, AFS_SEL))
#define ACC_SCALE_FACTOR (pow(2, AFS_SEL) / 16384.0)


/**
  * @brief
  * Address of accelerometer config register.
  * Bit 7: XA_ST
  * Bit 6: YA_ST
  * Bit 5: ZA_ST
  * Bits 4-3: AFS_SEL[1:0]
*/
#define ACC_CONFIG_REG 0x1C

/**
  * @brief
  * Address of the first register with accelerometer data.
  * The values are layed out in the order of X, Y, Z, with
  * 16 bits per axix in Big Endian (MSB first).
*/
#define ACC_REG_START 0x3B

// ======= GYROSCOPE ========= //

// Gyroscope range
#define FS_SEL 1
#define GYRO_SCALE_FACTOR (pow(2, FS_SEL) / 131.0)

/**
  * @brief
  * Address of the first register with gyroscope data.
  * The values are layed out in the order of X, Y, Z, with
  * 16 bits per axix in Big Endian (MSB first).
*/
#define GYRO_REG_START 0x43

/**
  * @brief
  * Address of gyroscope config register.
  * Bit 7: XG_ST
  * Bit 6: YG_ST
  * Bit 5: ZG_ST
  * Bits 4-3: FS_SEL[1:0]
*/
#define GYRO_CONFIG_REG 0x1B

#define INT_PIN_CFG_REG 0x37
#define I2C_BYPASS_EN 1

#define USER_CTRL_REG 0x6A
#define I2C_MST_EN 5

uint8_t MPU_init(const struct device *i2c_device);
uint8_t MPU_read_acc(int16_t output[]);
uint8_t MPU_read_gyro(int16_t output[]);

#endif