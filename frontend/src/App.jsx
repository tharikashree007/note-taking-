import React, { useEffect, useState } from 'react';
import Masonry from 'react-masonry-css';
import { NotebookText } from 'lucide-react';
import { fetchNotes, createNote, updateNote, deleteNote } from './api';
import NoteForm from './components/NoteForm';
import NoteCard from './components/NoteCard';

function App() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    try {
      const data = await fetchNotes();
      setNotes(data || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch notes:', err);
      setError('Could not establish connection to the backend.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async (noteData) => {
    try {
      const newNote = await createNote(noteData);
      setNotes([newNote, ...notes]);
    } catch (err) {
      console.error('Failed to create note:', err);
      alert('Error creating note');
    }
  };

  const handleUpdateNote = async (id, updatedData) => {
    try {
      const updatedNote = await updateNote(id, updatedData);
      setNotes(notes.map(note => note.id === id ? updatedNote : note));
    } catch (err) {
      console.error('Failed to update note:', err);
      alert('Error updating note');
    }
  };

  const handleDeleteNote = async (id) => {
    try {
      await deleteNote(id);
      setNotes(notes.filter(note => note.id !== id));
    } catch (err) {
      console.error('Failed to delete note:', err);
      alert('Error deleting note');
    }
  };

  const breakpointColumnsObj = {
    default: 4,
    1100: 3,
    700: 2,
    500: 1
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>
          <NotebookText size={32} color="#818cf8" />
          Notes
        </h1>
      </header>

      <main>
        <div style={{ marginBottom: '3rem', maxWidth: '600px', margin: '0 auto 3rem auto' }}>
          <NoteForm onAddNote={handleAddNote} />
        </div>

        {loading ? (
          <div className="loading-state">
            <p>Loading your notes...</p>
          </div>
        ) : error ? (
          <div className="empty-state">
            <p style={{ color: '#ef4444' }}>{error}</p>
          </div>
        ) : notes.length === 0 ? (
          <div className="empty-state">
            <NotebookText size={48} opacity={0.2} />
            <p>You haven't written any notes yet.</p>
          </div>
        ) : (
          <Masonry
            breakpointCols={breakpointColumnsObj}
            className="my-masonry-grid"
            columnClassName="my-masonry-grid_column"
          >
            {notes.map(note => (
               <NoteCard
                 key={note.id}
                 note={note}
                 onUpdate={handleUpdateNote}
                 onDelete={handleDeleteNote}
               />
            ))}
          </Masonry>
        )}
      </main>
    </div>
  );
}

export default App;
