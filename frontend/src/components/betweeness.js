import React, { useEffect, useState } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function Betweeness() {
    const [topBetween, setTopBetween] = useState(null);

    const fetchBetween = async () => {
        let fetched = await apiWrapper.getTopBetween()
        setTopBetween(fetched.data)
    }
    
    useEffect(() => {
        fetchBetween()
    }, [])

    return(
        <Table striped bordered>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Betweeness Score</th>
                    <th>Follower Count</th>
                </tr>
            </thead>
            <tbody>
                {topBetween !== null ? topBetween.slice(0, 10).map((user, idx) => {
                    return (
                        <tr key={idx}>
                            <td>{user['name']}</td>
                            <td>{user['score'].toFixed(4)}</td>
                            <td>{user['followers']}</td>
                        </tr>
                    )
                }) : null}
            </tbody>
        </Table>
    )
}

export default Betweeness;
