"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
pyinstaller myapp.spec
./dist/gistream/gistream --config bin/config/camera.json --inference bin/config/models_config.json --rules bin/config/rules.json