import React, { useEffect, useState } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function QTopics() {
    const [trendingTopics, setTrendingTopics] = useState(null);
    const [trendingQTopics, setTrendingQTopics] = useState(null)

    const fetchTopics = async () => {
        let fetched = await apiWrapper.getTrendTops()
        let qtops = await apiWrapper.getQTops()
        setTrendingTopics(fetched.data)
        setTrendingQTopics(qtops.data)
    }
    
    useEffect(() => {
        fetchTopics()
    }, [])

    return(
        <div id="qtable">
            <Table striped bordered>
                <thead>
                    <tr>
                        <th colSpan="2">Associated Q Topics</th>
                    </tr>
                </thead>
                <tbody>
                    {(trendingTopics !== null && trendingQTopics !== null) ? trendingTopics.map((topic, idx) => {
                        return (
                            <React.Fragment key={idx}>
                                <tr>
                                    <td colSpan="2"><b>{'Topic ' + idx}</b></td>
                                </tr>
                                {topic.map((t, i) => {
                                    return (
                                        <tr key={t + '' + i}>
                                            <td>{t}</td>
                                            <td>{trendingQTopics[idx][i]}</td>
                                        </tr>
                                    )
                                })}
                            </React.Fragment>
                        )
                    }) : null}
                </tbody>
            </Table>
        </div>
    )
}

export default QTopics;
