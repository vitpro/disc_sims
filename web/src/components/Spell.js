import React, { Component } from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';

const Container = styled.div`
    border: 1px solid lightgrey;
    border-radius: 2px;
    padding: 8px;
    margin-bottom: 8px;
`;

const grid = 8;

const getItemStyle = (isDragging, draggableStyle) => ({
  // some basic styles to make the items look a bit nicer
      userSelect: 'none',
      padding: grid * 2,
      margin: `0 ${grid}px 0 0`,

      // change background colour if dragging
      background: isDragging ? 'lightgrey' : 'grey',
      border: isDragging? 'solid red 2px' : '',
      // styles we need to apply on draggables
      ...draggableStyle,
});

export default class Spell extends Component {
    render() {
        const key = this.props.spell.id + '/' + this.props.index;
        return (
            <Draggable
                key={key}
                draggableId={key}
                index={this.props.index}
            >
                { (provided, snapshot) => (
                    <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        style={getItemStyle(
                            snapshot.isDragging,
                            provided.draggableProps.style
                        )}
                    >
                        {this.props.spell.name}
                    </div>

                )}
            </Draggable>
        );
    }
}