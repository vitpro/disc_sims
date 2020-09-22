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

const grid = 8;

const getItems = count =>
  Array.from({ length: count }, (v, k) => k).map(k => ({
    id: `item-${k}`,
    content: `item ${k}`,
  }));

const getListStyle = isDraggingOver => ({
  background: isDraggingOver ? 'lightblue' : 'lightgrey',
  display: 'flex',
  padding: grid,
  overflow: 'auto',
});

const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {
                'spells': []
            },
            items: getItems(6),
            loaded: false,
            placeholder: "Loading"
        };
        this.onDragEnd = this.onDragEnd.bind(this);
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
        // dropped outside the list
        if (!result.destination) {
            return;
        }

        const items = reorder(
            this.state.items,
            result.source.index,
            result.destination.index
        );

        this.setState({
            items,
        });
    }


    render() {
        return (
            <div>
                <Title>Title</Title>
                <DragDropContext onDragEnd={this.onDragEnd}>
                    <Droppable droppableId="droppable">
                        { (provided, snapshot) => (
                            <div
                                ref={provided.innerRef}
                                style={getListStyle(snapshot.isDraggingOver)}
                                {...provided.droppableProps}
                            >
                                {this.state.data.spells.map((spell, index) => (
                                    <Spell key={'spellid-' + spell.id} spell={spell} index={index} />
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
