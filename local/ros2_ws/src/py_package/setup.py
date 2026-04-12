from setuptools import find_packages, setup

package_name = 'py_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'talker = py_package.minimal_publisher:main',
            'listener = py_package.minimal_subscriber:main',
            'add_ints_service = py_package.minimal_service:main',
            'add_ints_client = py_package.minimal_client:main',
            'mini_param_node = py_package.minimal_parameter:main',
            'fibonacci_action_server = py_package.fibonacci_action_server:main',
            'fibonacci_action_client = py_package.fibonacci_action_client:main'
        ],
    },
)
