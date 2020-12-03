import React, { useEffect, useState } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function Louvain() {
    const [topLouvain, setTopLouvain] = useState([]);
    const [louvainStats, setLouvainStats] = useState(null);

    const fetchLouvain = async () => {
        let fetched = await apiWrapper.getTopLouvain()
        let stats = await apiWrapper.getLouvainStats()
        setTopLouvain(fetched.data)
        setLouvainStats(stats.data)
    }
    
    useEffect(() => {
        fetchLouvain()
    }, [])

    return(
        <Table striped bordered>
            <thead>
                <tr>
                    <th colSpan="10">Louvain Statistics</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>Community Count</b></td>
                    <td><b>Max</b></td>
                    <td><b>Mean</b></td>
                    <td><b>Min</b></td>
                    <td><b>50%</b></td>
                    <td><b>75%</b></td>
                    <td><b>90%</b></td>
                    <td><b>95%</b></td>
                    <td><b>99%</b></td>
                    <td><b>99.9%</b></td>
                </tr>
                {louvainStats !== null ? <tr>
                    <td>{louvainStats[0]['communityCount']}</td>
                    <td>{louvainStats[0]['communityDistribution']['max']}</td>
                    <td>{louvainStats[0]['communityDistribution']['mean']}</td>
                    <td>{louvainStats[0]['communityDistribution']['min']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p50']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p75']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p90']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p95']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p99']}</td>
                    <td>{louvainStats[0]['communityDistribution']['p999']}</td>
                </tr>: null}
                <tr>
                    <td colSpan="10"><b>Louvain Clusters</b></td>
                </tr>
                <tr>
                    <td colSpan="2"><b>Community Size</b></td>
                    <td colSpan="4"><b>Top Topics</b></td>
                    <td colSpan="4"><b>Top Users</b></td>
                </tr>
                {topLouvain !== null ? topLouvain.map((community, idx) => {
                    return (
                        <React.Fragment key={idx}>
                            <tr>
                                <td colSpan="2" rowSpan="3">{community['size']}</td>
                                <td colSpan="4">{community['topTopics'][0]}</td>
                                <td colSpan="4">{community['topUsers'][0]}</td>
                            </tr>
                            <tr>
                                <td colSpan="4">{community['topTopics'][1]}</td>
                                <td colSpan="4">{community['topUsers'][1]}</td>
                            </tr>
                            <tr>
                                <td colSpan="4">{community['topTopics'][2]}</td>
                                <td colSpan="4">{community['topUsers'][2]}</td>
                            </tr>
                        </React.Fragment>
                    )
                }) : null}
            </tbody>
        </Table>
    )
}

export default Louvain;
