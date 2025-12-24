"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Plus, MessageSquare, User, Trash2, MoreVertical, Share2, Pin, Edit2, GripVertical } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
  pinned?: boolean;
  order?: number;
}

interface ChatSidebarProps {
  isOpen: boolean;
  chatHistory: ChatHistory[];
  onNewChat?: () => void;
  onSelectChat?: (id: string) => void;
  onDeleteChat?: (id: string) => void;
  onPinChat?: (id: string) => void;
  onRenameChat?: (id: string, newTitle: string) => void;
  onShareChat?: (id: string) => void;
  onReorderChats?: (reordered: ChatHistory[]) => void;
  currentChatId?: string | null;
}

interface SortableChatItemProps {
  chat: ChatHistory;
  isActive: boolean;
  isEditing: boolean;
  editingTitle: string;
  onSelect: (id: string) => void;
  onPin: (id: string) => void;
  onRename: (id: string, newTitle: string) => void;
  onShare: (id: string) => void;
  onDelete: (id: string) => void;
  onStartEdit: () => void;
  onEditTitleChange: (title: string) => void;
  onSaveEdit: () => void;
  onCancelEdit: () => void;
}

function SortableChatItem({
  chat,
  isActive,
  isEditing,
  editingTitle,
  onSelect,
  onPin,
  onRename,
  onShare,
  onDelete,
  onStartEdit,
  onEditTitleChange,
  onSaveEdit,
  onCancelEdit,
}: SortableChatItemProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const canBlur = useRef(false);

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: chat.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  useEffect(() => {
    if (isEditing && inputRef.current) {
      // Use requestAnimationFrame to ensure DOM is ready
      requestAnimationFrame(() => {
        inputRef.current?.focus();
        requestAnimationFrame(() => {
          inputRef.current?.select();
        });
      });
    }
  }, [isEditing]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      onSaveEdit();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      onCancelEdit();
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`group relative flex items-center w-full rounded-md ${isActive ? 'bg-muted' : ''}`}
    >
      {/* Drag Handle */}
      <div
        className="w-8 shrink-0 flex items-center justify-center cursor-grab active:cursor-grabbing opacity-0 group-hover:opacity-100 transition-opacity"
        {...attributes}
        {...listeners}
      >
        <GripVertical className="h-4 w-4 text-muted-foreground" />
      </div>

      {isEditing ? (
        <div
          className="flex-1 flex items-center gap-3 py-2.5 px-3 pr-10 min-w-0"
          onClick={(e) => {
            // Prevent selecting the conversation while editing
            e.stopPropagation();
          }}
          onMouseDown={(e) => {
            // Prevent any parent handlers from interfering
            e.stopPropagation();
          }}
        >
          <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
          <div className="flex-1 min-w-0">
            <input
              ref={inputRef}
              type="text"
              value={editingTitle}
              onChange={(e) => onEditTitleChange(e.target.value)}
              onKeyDown={handleKeyDown}
              onMouseDown={(e) => e.stopPropagation()}
              className="w-full text-sm bg-transparent border-b border-primary outline-none"
            />
            <p className="text-xs text-muted-foreground truncate mt-0.5">{chat.timestamp}</p>
          </div>
        </div>
      ) : (
        <Button
          variant="ghost"
          className="flex-1 justify-start gap-3 h-auto py-2.5 px-3 pr-10 hover:bg-muted/50 min-w-0"
          onClick={() => onSelect(chat.id)}
        >
          <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
          <div className="flex-1 text-left min-w-0">
            <p className="text-sm truncate">{chat.title}</p>
            <p className="text-xs text-muted-foreground truncate">{chat.timestamp}</p>
          </div>
        </Button>
      )}

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="absolute right-2 h-8 w-8 shrink-0 opacity-0 group-hover:opacity-100 data-[state=open]:opacity-100 transition-opacity"
            onClick={(e) => e.stopPropagation()}
          >
            <MoreVertical className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" side="right" className="w-48">
          <DropdownMenuItem onClick={() => onShare(chat.id)}>
            <Share2 className="mr-2 h-4 w-4" />
            <span>Chia sẻ cuộc trò chuyện</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => onPin(chat.id)}>
            <Pin className="mr-2 h-4 w-4" />
            <span>Ghim</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={onStartEdit}>
            <Edit2 className="mr-2 h-4 w-4" />
            <span>Đổi tên</span>
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            onClick={() => onDelete(chat.id)}
            className="text-destructive focus:text-destructive"
          >
            <Trash2 className="mr-2 h-4 w-4" />
            <span>Xóa</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

export function ChatSidebar({
  isOpen,
  chatHistory,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  onPinChat,
  onRenameChat,
  onShareChat,
  onReorderChats,
  currentChatId
}: ChatSidebarProps) {
  // Lifted editing state
  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState("");

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Separate pinned and unpinned chats
  const pinnedChats = chatHistory.filter((chat) => chat.pinned);
  const unpinnedChats = chatHistory.filter((chat) => !chat.pinned);

  const handleDragEnd = (event: DragEndEvent, isPinned: boolean) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const sourceList = isPinned ? pinnedChats : unpinnedChats;
      const oldIndex = sourceList.findIndex((chat) => chat.id === active.id);
      const newIndex = sourceList.findIndex((chat) => chat.id === over.id);

      if (oldIndex !== -1 && newIndex !== -1) {
        const reordered = arrayMove(sourceList, oldIndex, newIndex);
        const finalList = isPinned
          ? [...reordered, ...unpinnedChats]
          : [...pinnedChats, ...reordered];
        onReorderChats?.(finalList);
      }
    }
  };

  const handleStartEdit = (chatId: string) => {
    const chat = chatHistory.find(c => c.id === chatId);
    if (chat) {
      // Delay to let dropdown close completely
      setTimeout(() => {
        setEditingChatId(chatId);
        setEditingTitle(chat.title);
      }, 150);
    }
  };

  const handleSaveEdit = () => {
    if (editingChatId && editingTitle.trim()) {
      const originalChat = chatHistory.find(c => c.id === editingChatId);
      if (originalChat && editingTitle.trim() !== originalChat.title) {
        onRenameChat?.(editingChatId, editingTitle.trim());
      }
    }
    setEditingChatId(null);
    setEditingTitle("");
  };

  const handleCancelEdit = () => {
    setEditingChatId(null);
    setEditingTitle("");
  };

  const renderChatItem = (chat: ChatHistory) => (
    <SortableChatItem
      key={chat.id}
      chat={chat}
      isActive={currentChatId === chat.id}
      isEditing={editingChatId === chat.id}
      editingTitle={editingChatId === chat.id ? editingTitle : chat.title}
      onSelect={onSelectChat || (() => { })}
      onPin={onPinChat || (() => { })}
      onRename={onRenameChat || (() => { })}
      onShare={onShareChat || (() => { })}
      onDelete={onDeleteChat || (() => { })}
      onStartEdit={() => handleStartEdit(chat.id)}
      onEditTitleChange={setEditingTitle}
      onSaveEdit={handleSaveEdit}
      onCancelEdit={handleCancelEdit}
    />
  );

  return (
    <div
      className={`${isOpen ? "w-80" : "w-0"} transition-all duration-300 bg-muted/50 flex flex-col h-screen overflow-hidden`}
    >
      <div className="p-3 shrink-0">
        <Button
          className="w-full justify-start gap-2 h-11"
          variant="outline"
          onClick={onNewChat}
        >
          <Plus className="h-4 w-4" />
          Cuộc trò chuyện mới
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto overflow-x-hidden px-2 min-h-0">
        {/* Pinned Section */}
        {pinnedChats.length > 0 && (
          <div className="py-2">
            <h3 className="text-xs font-semibold text-muted-foreground px-3 mb-2">ĐÃ GHIM</h3>
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={(e) => handleDragEnd(e, true)}
            >
              <SortableContext
                items={pinnedChats.map(c => c.id)}
                strategy={verticalListSortingStrategy}
              >
                <div className="space-y-1">
                  {pinnedChats.map(renderChatItem)}
                </div>
              </SortableContext>
            </DndContext>
          </div>
        )}

        {/* Unpinned Section */}
        {unpinnedChats.length > 0 && (
          <div className="py-2">
            {pinnedChats.length > 0 && (
              <h3 className="text-xs font-semibold text-muted-foreground px-3 mb-2">GẦN ĐÂY</h3>
            )}
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={(e) => handleDragEnd(e, false)}
            >
              <SortableContext
                items={unpinnedChats.map(c => c.id)}
                strategy={verticalListSortingStrategy}
              >
                <div className="space-y-1">
                  {unpinnedChats.map(renderChatItem)}
                </div>
              </SortableContext>
            </DndContext>
          </div>
        )}
      </div>

      <div className="p-3 shrink-0 border-t bg-muted/20">
        <Button variant="ghost" className="w-full justify-start gap-3 h-11">
          <User className="h-4 w-4" />
          <span className="text-sm">Tài khoản</span>
        </Button>
      </div>
    </div>
  );
}
