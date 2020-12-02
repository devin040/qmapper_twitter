import React, { useEffect, useState } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function PageRank() {
    const [topPageRank, setTopPageRank] = useState([]);

    const fetchPageRank = async () => {
        let fetched = await apiWrapper.getTopPageRank()
        setTopPageRank(fetched.data)
    }
    
    useEffect(() => {
        fetchPageRank()
    }, [])

    return(
        <Table striped bordered>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Page Rank Score</th>
                    <th>Follower Count</th>
                </tr>
            </thead>
            <tbody>
                {topPageRank.slice(0, 10).map((user, idx) => {
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

export default PageRank;
