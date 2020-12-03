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
                    <td>Community Count</td>
                    <td>Max</td>
                    <td>Mean</td>
                    <td>Min</td>
                    <td>50%</td>
                    <td>75%</td>
                    <td>90%</td>
                    <td>95%</td>
                    <td>99%</td>
                    <td>99.9%</td>
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
                    <td colSpan="10">Louvain Clusters</td>
                </tr>
                <tr>
                    <td colSpan="2">Community Size</td>
                    <td colSpan="4">Top Topics</td>
                    <td colSpan="4">Top Users</td>
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
