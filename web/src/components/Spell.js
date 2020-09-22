import React, { Component } from 'react';
import styled from 'styled-components';
import ReactDOM from 'react-dom';
import { Draggable } from 'react-beautiful-dnd';

const Container = styled.div`
    border: 1px solid lightgrey;
    border-radius: 2px;
    padding: 8px;
    margin-bottom: 8px;
`;

export default class Spell extends Component {
    render() {
        const key = 'spellid-' + this.props.spell.id;
        return (
            <Draggable key={key} draggableId={this.props.spell.id} index={this.props.index}>
                { (provided) => (
                    <div
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        ref={provided.innerRef}
                    >
                        {this.props.spell.name}
                    </div>

                )}
            </Draggable>
        );
    }
}