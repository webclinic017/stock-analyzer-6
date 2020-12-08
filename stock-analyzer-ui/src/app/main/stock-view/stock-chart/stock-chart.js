import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Highcharts from 'highcharts/highstock';
import HighchartsReact from 'highcharts-react-official';

import { SERVER_BASE_URL } from '../../../constants';

const StockChart = ({ id }) => {

  const [options, setOptions] = useState({
    chart: {
      height: '600px'
    },
    rangeSelector: {
      selected: 1
    },
    title: {
      text: id
    },
    yAxis: [
      {
        labels: {
          align: 'right',
          x: -3
        },
        title: {
          text: 'OHLC'
        },
        height: '75%',
        lineWidth: 2,
        resize: {
          enabled: true
        }
      },
      {
        labels: {
          align: 'right',
          x: -3
        },
        title: {
          text: 'Volume'
        },
        top: '80%',
        height: '20%',
        offset: 0,
        lineWidth: 2
      }
    ],
    tooltip: {
      split: true
    },
    series: [
      {
        type: 'candlestick',
        name: 'OHLC',
        data: [],
      },
      {
        type: 'column',
        name: 'Volume',
        data: [],
        yAxis: 1,
      }
    ],
    plotOptions: {
      candlestick: {
        color: 'green',
        upColor: 'red'
      }
    },
  });

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(`${SERVER_BASE_URL}/stock_view/get_ohlc?id=${id}`);
      const { data, name } = res.data;
      const ohlc = data.map(row => ([
        (new Date(row[0])).getTime(), ...row.slice(1, 5).map(item => parseFloat(item.toFixed(2)))
      ]));
      const volume = data.map(row => ([
        (new Date(row[0])).getTime(), parseFloat(row[5].toFixed(2))
      ]));
      setOptions({
        title: {
          text: `${id} - ${name}`
        },
        series: [
          {
            type: 'candlestick',
            name: 'OHLC',
            data: ohlc,
            groupPadding: 0,
            pointPadding: 0.14
          },
          {
            type: 'column',
            name: 'Volume',
            data: volume,
            yAxis: 1,
            groupPadding: 0,
            pointPadding: 0.1
          }
        ]
      });
    };
    fetchData();
  }, [id]);

  return (
    <div id='chart'>
      <HighchartsReact
        highcharts={Highcharts}
        constructorType={'stockChart'}
        options={options}
      />
    </div>
  );
}

export default StockChart;