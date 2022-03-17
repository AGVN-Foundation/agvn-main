import React from 'react';
import { Chart, Interval, Tooltip } from 'bizcharts';

interface ContributeChartProps {
  data: Array<number>;
  width: number;
}

export default function ContributeChart({ data, width }: ContributeChartProps) {

  React.useEffect(() => {
    getData()
  }, [width])


  function getData() {
    var newData: { date: string; contribution: number; }[] = [];
    var option = {
      day: 'numeric',
      month: 'numeric'
    }
    data.forEach((value, index) => {
      let newDate = new Date();
      newDate.setDate(newDate.getDate() - 30 + index)
      newData.push({ "date": newDate.toLocaleDateString('en-AU'), "contribution": value });
    })
    return newData;
  }

  return (
    <Chart data={getData()} width={width} height={400} widthautofit={true} interactions={['active-region']} padding='auto' style={{}}>
      <Interval position="date*contribution" />
      <Tooltip shared />
    </Chart>
  )
}