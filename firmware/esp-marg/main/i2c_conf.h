#ifndef I2C_CONF_H
#define I2C_CONF_H

#define I2C_NUM 0
#define I2C_MASTER_NUM 0 
#define I2C_TIMEOUT_MS (1000)
// #define I2C_TIMEOUT (I2C_TIMEOUT_MS / (portTICK_PERIOD_MS))
#define I2C_TIMEOUT 10000
#define I2C_MASTER_SCL_IO           9      /*!< GPIO number used for I2C master clock */
#define I2C_MASTER_SDA_IO           8      /*!< GPIO number used for I2C master data  */
#define I2C_MASTER_FREQ_HZ          400000                     /*!< I2C master clock frequency */
#define I2C_MASTER_TX_BUF_DISABLE   0                          /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE   0                          /*!< I2C master doesn't need buffer */
#define I2C_MASTER_TIMEOUT_MS       1000

#endif