from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'diffdrive_mujoco'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    
    # YEH ADD KARO:
    ('lib/python3.10/site-packages/diffdrive_mujoco', [
        'diffdrive_mujoco/differentialdrive.xml'
    ]),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rahul',
    maintainer_email='rahul@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
entry_points={
    'console_scripts': [
        'diffdrive_node = diffdrive_mujoco.diffdrive_ros2:main',
    ],
},
)
