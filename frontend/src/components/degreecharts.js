import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import {
    Container,
    Row,
    Col
} from 'reactstrap';

import apiWrapper from '../api'


function DegreeCharts() {
    const [Indegree, setIndegree] = useState([]);
    const [Outdegree, setOutdegree] = useState([]);


    const toggleData = async e => {
        let indegree = await apiWrapper.getIndegreeDistro();
        setIndegree(() => indegree.data)

        let outdegree = await apiWrapper.getOutdegreeDistro();
        setOutdegree(() => outdegree.data);
    }

    useEffect(() => {
        toggleData()
    }, [])

    return(
        <Container>
            <Row>
                <Col>
                    <LineChart width={400} height={300} data={Indegree}
                        margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                    <XAxis dataKey="degree"/>
                    <YAxis/>
                    <CartesianGrid strokeDasharray="3 3"/>

                        <Legend />
                        <Line name="Indegree" type="monotone" dataKey="pct" stroke="#8884d8" dot={false}/>
                    </LineChart>
                 </Col>
                 <Col>
                    <LineChart width={400} height={300} data={Outdegree}
                                margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                        <XAxis dataKey="degree"/>
                        <YAxis/>
                        <CartesianGrid strokeDasharray="3 3"/>

                        <Legend />
                        <Line name="Outdegree" type="monotone" dataKey="pct" stroke="#8884d8" dot={false}/>
                    </LineChart>
                 </Col>
             </Row>
        </Container>
    )
}

export default DegreeCharts;