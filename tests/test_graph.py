import textwrap
from pathlib import Path

import pytest

from settings import Colors, tick
from pychart.pychart import Chart

root = Path(__file__).cwd()
data = root / 'data'


@pytest.fixture
def default_graph():
    return Chart()


class TestGraph:
    def test_build_basic_row(self, default_graph):
        expected = f' asdf: {Colors.red.value}{tick * 5} {Colors.reset.value}32.3'
        actual = default_graph._build_row(
            index='asdf',
            length=5,
            color=Colors.red.value,
            tick=tick,
            number_of_blocks=5,
            data_value=32.3,
        )
        assert actual == expected

    def test_build_stacked_row(self, default_graph):
        expected = f'     : {Colors.red.value}{tick * 5} {Colors.reset.value}32.3'
        actual = default_graph._build_row(
            index='',
            length=5,
            color=Colors.red.value,
            tick=tick,
            number_of_blocks=5,
            data_value=32.3,
        )
        assert actual == expected

    def test_build_ex1_basic_bar_chart(self):
        expected = '2007: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 183.32\n2008: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 231.23\n2009: ▇▇ 16.43\n2010: ▇▇▇▇▇ 50.21\n2011: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 508.97\n2012: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 212.05\n2014: ▏ 1.0'
        chart = Chart(filename=data / 'ex1.dat', delimiter=' ')
        actual = str(chart)
        assert expected == actual

    def test_build_ex2_basic_bar_chart(self):
        expected = '    label: ▇▇ 2.0\nlonglabel: ▇▇▇ 3.0\n      foo: ▇▇▇▇ 4.0\n barrific: ▇▇▇▇▇ 5.0\n      wut: ▇▇▇▇▇▇ 6.0'
        chart = Chart(filename=data / 'ex2.dat', delimiter=' ')
        actual = str(chart)
        assert expected == actual

    def test_build_ex4_colored_stacked_chart(self):
        expected = f'''{Colors.blue.value}▇ Boys {Colors.red.value}▇ Girls {Colors.reset.value}

2007: {Colors.blue.value}▇▇▇▇▇▇▇▇▇▇▇ {Colors.reset.value}183.32
    : {Colors.red.value}▇▇▇▇▇▇▇▇▇▇▇ {Colors.reset.value}190.52
2008: {Colors.blue.value}▇▇▇▇▇▇▇▇▇▇▇▇▇▇ {Colors.reset.value}231.23
    : {Colors.red.value}▏ {Colors.reset.value}5.0
2009: {Colors.blue.value}▇ {Colors.reset.value}16.43
    : {Colors.red.value}▇▇▇ {Colors.reset.value}53.1
2010: {Colors.blue.value}▇▇▇ {Colors.reset.value}50.21
    : {Colors.red.value}▏ {Colors.reset.value}7.0
2011: {Colors.blue.value}▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ {Colors.reset.value}508.97
    : {Colors.red.value}▇ {Colors.reset.value}10.45
2012: {Colors.blue.value}▇▇▇▇▇▇▇▇▇▇▇▇ {Colors.reset.value}212.05
    : {Colors.red.value}▇ {Colors.reset.value}20.2
2014: {Colors.blue.value}▇▇ {Colors.reset.value}30.0
    : {Colors.red.value}▇ {Colors.reset.value}20.0'''
        chart = Chart(filename=data / 'ex4.dat', delimiter=',', width=30, colors=['blue', 'red'])
        actual = str(chart)
        assert actual == expected