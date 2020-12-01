import React, { useState, useEffect } from 'react';
import { 
    Table
} from 'reactstrap';

import apiWrapper from '../api'


function TopTrending() {
    const [topTrending, setTopTrending] = useState([]);

    const fetchTrending = async () => {
        let fetched = await apiWrapper.getTopTrending()
        setTopTrending(fetched.data)
    }
    
    useEffect(() => {
        fetchTrending()
    }, [])

    return(
        <Table striped bordered>
            <tbody>
                {topTrending.slice(0, 10).map((topic, idx) => {
                    return (
                        <tr key={idx}>
                            <td>{topic['topic']}</td>
                        </tr>
                    )
                })}
            </tbody>
        </Table>
    )
}

export default TopTrending;
