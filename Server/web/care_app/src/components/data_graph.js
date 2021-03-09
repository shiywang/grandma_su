import React from 'react';
import { ResponsiveLine } from '@nivo/line'

export class MyGraph extends React.Component {
    render(){
        return(
        <ResponsiveLine
            data={[
                {
                    data: [
                        { x: 0, y: 7 },
                        { x: 1, y: 5 },
                        { x: 2, y: 11 },
                        { x: 3, y: 9 },
                        { x: 4, y: 13 },
                        { x: 7, y: 16 },
                        { x: 9, y: 12 },
                    ],
                },
            ]}
            margin={{ top: 50, right: 50, bottom: 50, left: 60 }}
            xScale={{ type: 'linear' }}
            yScale={{ type: 'linear', min: 'auto', max: 'auto', stacked: true, reverse: false }}
            yFormat=" >-.2f"
            curve="natural"
            colors={{ scheme: 'nivo' }}
            axisBottom={{
                legend: 'time',
                legendOffset: 36,
                legendPosition: 'middle'
            }}
            axisLeft={{
                legend: this.props.data.device_type,
                legendPosition: 'middle',
                legendOffset: -36,
            }}
            pointSize={10}
            pointColor={{ theme: 'background' }}
            pointBorderWidth={2}
            pointBorderColor={{ from: 'serieColor' }}
            pointLabelYOffset={-12}
            useMesh={true}
        />
        );
    }

}