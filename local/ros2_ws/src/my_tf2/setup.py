from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'my_tf2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chuongnguyen',
    maintainer_email='chuong.nguyen@cybercore.co.jp',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'static_tf2_broadcaster = my_tf2.static_tf2_broadcaster:main',
            'turtle_tf2_broadcaster = my_tf2.turtle_tf2_broadcaster:main',
            'turtle_tf2_listener = my_tf2.turtle_tf2_listener:main',
            'carrot_tf2_broadcaster = my_tf2.carrot_tf2_broadcaster:main',
            'turtle_tf2_msg_broadcaster = my_tf2.turtle_tf2_msg_broadcaster:main',
            'turtle_tf2_msg_filter = my_tf2.turtle_tf2_msg_filter:main',
        ],
    },
)
