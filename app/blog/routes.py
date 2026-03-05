from flask import render_template, request, abort
from app.blog import blog_bp
from app.models import BlogPost
from sqlalchemy import or_


@blog_bp.route('/')
def blog_list():
    """Blog listing page with pagination and search"""
    page = request.args.get('page', 1, type=int)
    per_page = 9

    # Search query
    search_query = request.args.get('q', '')

    # Build query
    query = BlogPost.query.filter_by(is_published=True)

    if search_query:
        search_filter = or_(
            BlogPost.title.contains(search_query),
            BlogPost.subtitle.contains(search_query),
            BlogPost.content.contains(search_query)
        )
        query = query.filter(search_filter)

    # Get paginated results
    posts = query.order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get all categories for filter
    categories = BlogPost.query.with_entities(BlogPost.category).filter(
        BlogPost.is_published == True,
        BlogPost.category.isnot(None)
    ).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template('blog/blog_list.html',
                         posts=posts,
                         categories=categories,
                         search_query=search_query)


@blog_bp.route('/category/<category>')
def blog_category(category):
    """Blog posts filtered by category"""
    page = request.args.get('page', 1, type=int)
    per_page = 9

    posts = BlogPost.query.filter_by(
        is_published=True,
        category=category
    ).order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    if not posts.items and page == 1:
        abort(404)

    return render_template('blog/blog_list.html',
                         posts=posts,
                         current_category=category)


@blog_bp.route('/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Increment view counter
    post.increment_views()

    # Get related posts (same category)
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.is_published == True,
        BlogPost.category == post.category
    ).order_by(BlogPost.published_at.desc()).limit(3).all()

    return render_template('blog/blog_post.html',
                         post=post,
                         related_posts=related_posts)
