import React, { Component, Fragment } from "react";
import { render } from "react-dom";
import styled, { css } from 'styled-components';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import ReactDOM from 'react-dom';
import Select, { defaultTheme } from 'react-select';
import Spell from './Spell';
import Footer from './Footer';
import Header from './Header';
import ProgressContainer from './ProgressContainer';
import LandingContainer from './LandingContainer';
import TalentPicker from './TalentPicker';
import RacePicker from './RacePicker';
import SpecPicker from './SpecPicker';

const Container = styled.div`
    margin: 20px;
    border: 2px solid lightgrey;
    border-radius: 2px;
`;

const Button = styled.button`
    margin-left: 10px;
`;

const StagesContainer = styled.div`
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
            sim_data: {
                spec: 'disc',
                selected_talents: [],
                sequence: [],
                targets: [],
            },
            sequence: [],
            targets: [],
            loaded: false,
            selected_spell: null,
            placeholder: "Loading",
            progressBarSteps: [
                14, 28, 100
            ],
            isSimming: true, // flag to indicate that report is being generated
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

    updateSelectedTalents = talents => {
        const sim_data = this.state.sim_data;
        sim_data.selected_talents = talents;
        this.setState({
            ...this.state,
            sim_data: sim_data,
        });
    };

    // TODO implement this
    specChangeHandler = spec => {
        console.log(spec);
    };

    // TODO implement this
    raceChangeHandler = race => {
        console.log(race);
    };

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

    processSims = () => {
        // TODO redirect? or let django redirect later?

        // construct spell sequence coupled with targets
        const spell_sequence = this.state.sequence.map((spell) => {
           return [spell, 0] /*this.state.targets[index]]*/; // TODO reconsider targeting
        });
        console.log(spell_sequence);
        const requestBody = {
            spell_sequence: spell_sequence,
            player_stats: [],
            player_talents: [],
            active_buffs: [],
            simulate: false,
        };

        const requestOptions = {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify(requestBody),
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        };
        fetch("/submit-sim/", requestOptions)
            .then(resp => {
                if (resp.status > 400) {
                    return { placeholder: "error submitting sim data"}
                }
            })
            .then(data => {
                console.log(data);
            })
    };

    render() {
        const selectSpellListOptions = this.state.data.spells.map(spell => {
            return { value: spell.id, label: spell.name }
        });
        return (
            <div className="wrapper">
                <Header />
                <LandingContainer />
                <div className="mainContainer">
                    <ProgressContainer barCompleted={14} barDisplayPercentage={this.state.isSimming} />
                    <StagesContainer>

                        <div className="characterDetailsContainer">
                            <div className="characterDetailsColumn">
                                <div className="raceSpecContainer">
                                    <div className="racePickerContainer">
                                        <h2 className="midTitle">Race</h2>
                                        <RacePicker
                                            raceChangeHandler={this.raceChangeHandler}
                                        >
                                        </RacePicker>
                                    </div>

                                    <div className="specPickerContainer">
                                        <h2 className="midTitle">Spec</h2>
                                        <SpecPicker
                                            specChangeHandler={this.specChangeHandler}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <h2 className="midTitle">Meaningful Choice</h2>

                                </div>
                            </div>
                            <div className="characterDetailsColumn">
                                <TalentPicker spec={this.state.sim_data.spec} updateTalentsHandler={this.updateSelectedTalents}>
                                </TalentPicker>
                            </div>
                        </div>

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
                        <Button
                            onClick={this.processSims}
                        >
                            Process
                        </Button>
                    </StagesContainer>
                </div>
                <Footer/>
            </div>
        );
    }
}

export default App;

ReactDOM.render(<App />, document.getElementById('app'));
