# Internal Reporting Tool

This python program defines three PostgreSQL queries used to answer three questions about a news website:
1. The top three articles by number of views
2. The top three authors based on number of views
3. The days which had an error rate of over 1%
The results are printed to a .txt file for analysis.
___
## Getting Started

These instructions will explain how to begin using this program.
___
### Prerequisites

This program requires Python3, Virtual Box, and Vagrant to run.
___
### Installation

Install [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html).

**Windows users**: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

Next, fork and clone the [Virtual Machine configuration repository](https://github.com/udacity/fullstack-nanodegree-vm) from Github.
In the terminal, cd to the new vagrant folder and type:
```
vagrant up
```
to configure the VM. After it is finished, type:
```
vagrant ssh```
to log in to the VM.
After that, download the [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and type:
```python
psql -d news -f newsdata.sql
```
to generate the database.
___
### Execution

Inside the VM, type:
```
cd /vagrant/logs_analysis
```
and then:
```
python3 internal-reporting-tool.py
```
to run the reporting tool.
The results are written to the .txt file in the logs_analysis folder.
___
### License

MIT License

Copyright (c) 2018 [Miles Whitman](@mwhitman189)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
