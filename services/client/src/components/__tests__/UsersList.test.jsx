import React from 'react'
import { shallow } from 'enzyme'
import renderer from 'react-test-renderer';

import UsersList from '../UsersList'

const users = [
    {
        'active': true,
        'email': 'hermanmu@gmail.com',
        'id': 1,
        'username': 'michael1zC00L'
    },
    {
        'active': true,
        'email': 'billybob@yahoo.com',
        'id': 2,
        'username': 'billybob560'
    }
]

test('UsersList render properly', () => {
    const wrapper = shallow(<UsersList users={users}/>)
    const element = wrapper.find('h4')
    expect(element.length).toBe(2)
    expect(element.get(0).props.children).toBe('michael1zC00L')
})

test('UsersList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON()
    expect(tree).toMatchSnapshot()
})