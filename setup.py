import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'qubot'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share/' + package_name, 'config'), glob(os.path.join('config', '*.*'))),
        (os.path.join('share/' + package_name, 'description'), glob(os.path.join('description', '*.*'))),
        (os.path.join('share/' + package_name, 'launch'), glob(os.path.join('launch', '*launch.py'))),
        
    ],
    install_requires=['setuptools',
                      'pymodbus'],
    zip_safe=True,
    maintainer='cmoralesd',
    maintainer_email='claudio.morales@edutecnica.cl',
    description='Paquete base para el control de qubot en entorno de simulación',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'zlac8015d_bridge = qubot.zlac8015d_bridge:main',
            'camera_publisher = qubot.camera_publisher:main',
            'camera_subscriber = qubot.camera_subscriber:main',
        ],
    },
)
