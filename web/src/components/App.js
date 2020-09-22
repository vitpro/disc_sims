import React, { Component } from "react";
import { render } from "react-dom";
import styled, { css } from 'styled-components';
import Spell from './Spell';

const Container = styled.div`
    margin: 8px;
    border: 1px solid lightgrey;
    border-radius: 2px;
`;
const Title = styled.h3`
    padding: 8px;
`;
const SpellQueue = styled.div`
    padding: 8px;
`;

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {
                'spells': []
            },
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        const requestOptions = {
            method: 'GET',
        };
        fetch("/get_spells", requestOptions)
            .then(resp => {
                if (resp.status > 400) {
                    return this.setState(() => {
                        return { placeholder: "Error loading spell data"};
                    });
                }
                return resp.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        const spell_names = this.state.data.spells.map(spell => <Spell key={spell.id} spell={spell} />);

        return (
            <Container>
                <Title>Title</Title>
                <SpellQueue>{spell_names}</SpellQueue>
            </Container>
        );
    }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);