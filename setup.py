from setuptools import setup

setup(name='testpipeline',
      description='simple gaia python pipeline example',
      packages=['pipeline'],
      author='pipelineauthor',
      author_email='pipelineauthor@mail.com',
      install_requires=[
            'gaiasdk>=0.0.16',
            'GitPython==3.1.27',
            'python-owasp-zap-v2.4==0.0.14',
            'selenium==3.14',
            'requests',
            'selenium-requests==1.3'
      ])
