import React, { useEffect, useState } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function PageRankWeight() {
    const [topPageRankW, setTopPageRankW] = useState([]);

    const fetchPageRankW = async () => {
        let fetched = await apiWrapper.getTopPageRankW()
        setTopPageRankW(fetched.data)
    }
    
    useEffect(() => {
        fetchPageRankW()
    }, [])

    return(
        <Table striped bordered>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Page Rank Weighted Score</th>
                    <th>Follower Count</th>
                </tr>
            </thead>
            <tbody>
                {topPageRankW.slice(0, 10).map((user, idx) => {
                    return (
                        <tr key={idx}>
                            <td>{user['name']}</td>
                            <td>{user['score'].toFixed(4)}</td>
                            <td>{user['followers']}</td>
                        </tr>
                    )
                })}
            </tbody>
        </Table>
    )
}

export default PageRankWeight;
