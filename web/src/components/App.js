import React, { Component, Fragment } from "react";
import { render } from "react-dom";
import styled, { css } from 'styled-components';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import ReactDOM from 'react-dom';
import Select, { defaultTheme } from 'react-select';
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

const Button = styled.button`
    
    margin-left: 10px;
`;

const grid = 8;

const getListStyle = isDraggingOver => ({
    background: isDraggingOver ? 'lightgrey' : 'lightgrey',
    display: 'flex',
    padding: grid,
    overflow: 'auto',
    width: '800px',
    height: '80px',
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
            sequence: [],
            loaded: false,
            selected_spell: null,
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
            this.state.sequence,
            result.source.index,
            result.destination.index
        );

        // update state to keep track of ordering
        this.setState({
            ...this.state,
            sequence: items,
        });
    }

    handleSelectChange = selected => {
        this.setState({
            ...this.state,
            selected_spell: selected,
        });
    };

    addNewSpellToSequence = () => {
        // if none selected - do nothing
        if (this.state.selected_spell) {
            const spellToAdd = this.state.data.spells.find(spell => spell.id === this.state.selected_spell.value);
            const seq = this.state.sequence.slice();
            seq.push(spellToAdd);
            this.setState({
                ...this.state,
                sequence: seq,
            })
        }
    };

    render() {
        const selectSpellListOptions = this.state.data.spells.map(spell => {
            return { value: spell.id, label: spell.name }
        });
        return (
            <div>
                <Title>Title</Title>
                <Container>
                    Add spell:
                    <Select
                        className="basic-single"
                        classNamePrefix="select"
                        options={selectSpellListOptions}
                        onChange={this.handleSelectChange}
                    />
                    <Button
                        onClick={this.addNewSpellToSequence}
                    >
                        Add
                    </Button>
                </Container>
                <DragDropContext onDragEnd={this.onDragEnd}>
                    <Droppable droppableId="droppable" direction="horizontal">
                        { (provided, snapshot) => (
                            <div
                                ref={provided.innerRef}
                                style={getListStyle(snapshot.isDraggingOver)}
                                {...provided.droppableProps}
                            >
                                {this.state.sequence.map((spell, index) => (
                                    <Spell key={spell.id + '/' + index}
                                           spell={spell} index={index} />
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
