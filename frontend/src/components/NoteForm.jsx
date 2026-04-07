import React, { useState } from 'react';
import { Plus } from 'lucide-react';

const NoteForm = ({ onAddNote }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() && !content.trim()) return;
    
    onAddNote({
      title: title.trim() || 'Untitled',
      content: content.trim()
    });
    
    setTitle('');
    setContent('');
  };

  return (
    <form className="note-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="note-input-title"
        placeholder="Note title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="note-input-content"
        placeholder="Write your note down..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={3}
      />
      <div className="note-form-actions">
        <button type="submit" className="btn">
          <Plus size={18} /> Add Note
        </button>
      </div>
    </form>
  );
};

export default NoteForm;
