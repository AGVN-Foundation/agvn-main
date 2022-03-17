import React from 'react';
import { Chart, Interval, Tooltip, Line } from 'bizcharts';

export interface GCoinChartProps {
  data: Array<number>;
  width: number;
}

export default function GCoinChart({ data, width }: GCoinChartProps) {

  React.useEffect(() => {
    getData()
  }, [width])


  function getData() {
    var newData: { date: string; value: number; }[] = [];
    var option = {
      day: 'numeric',
      month: 'numeric'
    }
    data.forEach((value, index) => {
      let newDate = new Date();
      newDate.setDate(newDate.getDate() - 30 + index)
      newData.push({ "date": newDate.toLocaleDateString('en-AU'), "value": value });
    })
    return newData;
  }

  return (
    <Chart data={getData()} width={width} height={400} widthautofit={true} interactions={['active-region']} padding='auto' style={{}}>
      <Interval position="date*value" />
      <Line position="date*value" size={1} color={'city'} />
      <Tooltip shared />
    </Chart>
  )
}