import React, { Component } from "react";
import { render } from "react-dom";
import styled, { css } from 'styled-components';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import ReactDOM from 'react-dom';
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

    onDragEnd(result) {
        console.log('xd' + result);
    };


    render() {
        return (
            <div>
                <Title>Title</Title>
                <DragDropContext onDragEnd={this.onDragEnd}>
                    <Droppable droppableId="droppable">
                        { (provided) => (
                            <div
                                ref={provided.innerRef}
                                {...provided.droppableProps}
                            >
                                {this.state.data.spells.map((spell, index) => (
                                    <Spell key={'spellid-' + spell.id} spell={spell} index={index}/>
                                ))}
                                {provided.placeholder}
                            </div>
                        )}
                    </Droppable>
                </DragDropContext>
            </div>
        );
    }
}

export default App;

ReactDOM.render(<App />, document.getElementById('app'));
// const container = document.getElementById("app");
// render(<App />, container);
