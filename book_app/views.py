from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from user_app.models import EntityChoices, User
from rest_framework.generics import (
    ListAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    BookModel,
    LibraryModel,
)
from .serializers import (
    BookListSerializer,
    RenewAndHistoryBookSerializer,
    BorrowBookSerializer,
    ReturnedBookSerializer,
)
from .permissions import (
    StudentPermissions, 
    LibrarianPermissions,
)
from .filterset import (
    BookFilter,
    HistoryFilter
)

# Create your views here.

class ListAllBooks(ListAPIView):
    queryset = BookModel.objects.all()
    permission_classes = []
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

class BorrowedBooksList(ListAPIView):
    queryset = LibraryModel.objects.all()
    permission_classes = [StudentPermissions|LibrarianPermissions]
    serializer_class = RenewAndHistoryBookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryFilter

    def get_queryset(self):
        if self.request.user.entity == EntityChoices.STUDENT:
            self.queryset = self.queryset.filter(borrowed_by=self.request.user)
        return self.queryset

@extend_schema(
    request=RenewAndHistoryBookSerializer(many=True)
)    
class RenewedBooks(APIView):
    queryset = LibraryModel.objects.all()
    permission_classes = [StudentPermissions]
    serializer_class = RenewAndHistoryBookSerializer

    def validate(self, borrowed_books):
        for book in borrowed_books:
            book_title = book.book.title
            if book.borrowed_by != self.request.user:
                raise PermissionDenied(_(f'{book_title} book was not borrowed by this user.'))
            if book.status == LibraryModel.BookStatusEnum.RETURNED:
                raise PermissionDenied(_(f"Book {book_title} has been returned, need to ask librarian to register again."))
            if book.status == LibraryModel.BookStatusEnum.RENEWED:
                raise PermissionDenied(_(f"This user has been renewed {book_title} book, please return the book."))
        return True

    def patch(self, request, *args, **kwargs):
        payloads = request.data
        ids =  [data['id'] for data in payloads]
        borrowed_books = LibraryModel.objects.filter(id__in=ids)
        if borrowed_books.exists():
            if self.validate(borrowed_books):
                borrowed_books.update(status=LibraryModel.BookStatusEnum.RENEWED)
                serializer = RenewAndHistoryBookSerializer(LibraryModel.objects.filter(id__in=ids), many=True)
                return Response(serializer.data)
        else:
            raise NotFound(_("Borrowed books not found."))

@extend_schema(
    request=BorrowBookSerializer(many=True)
)
class BorrowBooks(APIView):
    queryset = LibraryModel.objects.all()
    permission_classes = [LibrarianPermissions]
    serializer_class = BorrowBookSerializer

    def validate_borrowed_books(self, attrs):
        borrowed_books = LibraryModel.objects.filter(borrowed_by__id=attrs[0].get('borrowed_by')).exclude(status=LibraryModel.BookStatusEnum.RETURNED)
        if borrowed_books.exists():
            if (borrowed_books.count() >= 10) or (borrowed_books.count() + len(attrs) > 10):
                raise PermissionDenied(_("Already reach max. capacity of borrowed books."))
        return True
    
    def validate_books(self, book_id):
        book = get_object_or_404(BookModel, pk=book_id)
        if book.available_copy -1 < 0:
            raise PermissionDenied(_(f"we have availbility shortage in {book.title}."))
        return book

    def post(self, request, *args, **kwargs):
        payloads = request.data
        cleaned_data = []
        self.validate_borrowed_books(payloads)
        for payload in payloads:
            payload['book'] = self.validate_books(payload['book'])
            payload['borrowed_by'] = get_object_or_404(User, pk=payload['borrowed_by'])
            data = LibraryModel(**payload, created_by=self.request.user)
            cleaned_data.append(data)
        result = LibraryModel.objects.bulk_create(cleaned_data)
        serializer = BorrowBookSerializer(result, many=True)
        return Response(serializer.data)

@extend_schema(
    request=ReturnedBookSerializer(many=True)
)
class ReturnBook(APIView):
    queryset = LibraryModel.objects.all()
    permission_classes = [LibrarianPermissions]
    serializer_class = ReturnedBookSerializer

    def patch(self, request, *args, **kwargs):
        payloads = request.data
        ids =  [data['id'] for data in payloads]
        borrowed_books = LibraryModel.objects.filter(id__in=ids)
        borrowed_books.update(status=LibraryModel.BookStatusEnum.RETURNED)
        serializer = ReturnedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data)