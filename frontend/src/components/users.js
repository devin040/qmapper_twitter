import React, { useState, useEffect } from 'react';
import { 
    Container, 
    Table, 
    Dropdown, 
    DropdownToggle, 
    DropdownMenu, 
    DropdownItem 
} from 'reactstrap';

import apiWrapper from '../api'


function Users() {
    const [topUsers, setTopUsers] = useState([]);
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const toggle = () => setDropdownOpen(prevState => !prevState);

    useEffect(() => {
        async function fetchTopUsers() {
          let topUsers = await apiWrapper.getTopUsers();
          setTopUsers(() => topUsers.data);
        }
        fetchTopUsers();
    }, [])

    return(
        <Container>
            <Table bordered>
                <thead>
                    <tr>
                    <th>Top Users</th>
                    <th>
                        <Dropdown isOpen={dropdownOpen} toggle={toggle}>
                        <DropdownToggle caret>
                            Filter
                        </DropdownToggle>
                        <DropdownMenu>
                            <DropdownItem>Filter 1</DropdownItem>
                        </DropdownMenu>
                        </Dropdown>
                    </th>
                    </tr>
                </thead>

                <tbody>
                    {topUsers.slice(0, 10).map((user, idx) => {
                        return (
                            <tr key={idx}>
                                <td colSpan="2">{user.username}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
        </Container>
    )
}

export default Users;
