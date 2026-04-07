import React, { useState } from 'react';
import { Trash2, Edit2, Check, X } from 'lucide-react';

const NoteCard = ({ note, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(note.title);
  const [editedContent, setEditedContent] = useState(note.content);

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const handleSave = () => {
    onUpdate(note.id, {
      title: editedTitle,
      content: editedContent
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedTitle(note.title);
    setEditedContent(note.content);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="note-card">
        <input 
          className="note-input-title" 
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
          autoFocus
        />
        <textarea 
          className="note-input-content" 
          value={editedContent}
          onChange={(e) => setEditedContent(e.target.value)}
          rows={4}
        />
        <div className="note-card-footer">
          <span>Editing...</span>
          <div className="note-actions" style={{ opacity: 1 }}>
            <button className="icon-btn" onClick={handleSave} title="Save">
              <Check size={16} />
            </button>
            <button className="icon-btn" onClick={handleCancel} title="Cancel">
              <X size={16} />
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="note-card">
      {note.title && <h3 className="note-card-title">{note.title}</h3>}
      {note.content && <div className="note-card-content">{note.content}</div>}
      <div className="note-card-footer">
        <span>{formatDate(note.created_at)}</span>
        <div className="note-actions">
          <button className="icon-btn" onClick={() => setIsEditing(true)} title="Edit Note">
            <Edit2 size={16} />
          </button>
          <button className="icon-btn delete" onClick={() => onDelete(note.id)} title="Delete Note">
            <Trash2 size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default NoteCard;
